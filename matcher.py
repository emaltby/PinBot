import re
import difflib

STOP_WORDS = {"the", "a", "an", "pinball", "machine", "pin", "game"}

def normalize_text(text):
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Replace punctuation and special characters with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_tokens(text, remove_stops=False):
    normalized = normalize_text(text)
    tokens = normalized.split()
    if remove_stops:
        tokens = [t for t in tokens if t not in STOP_WORDS]
    return tokens

def fuzzy_token_match(target_token, listing_tokens, threshold=0.85):
    for l_token in listing_tokens:
        if target_token == l_token:
            return True
        if len(target_token) > 3 and len(l_token) > 3:
            if difflib.SequenceMatcher(None, target_token, l_token).ratio() >= threshold:
                return True
    return False

def is_machine_match(target_machine, listing_title, fuzzy_threshold=0.82):
    norm_target = normalize_text(target_machine)
    norm_title = normalize_text(listing_title)
    
    if not norm_target or not norm_title:
        return False

    # 1. Exact or normalized substring match
    if norm_target in norm_title:
        return True

    # 2. Full string fuzzy ratio
    full_ratio = difflib.SequenceMatcher(None, norm_target, norm_title).ratio()
    if full_ratio >= fuzzy_threshold:
        return True

    # 3. Token-based analysis
    target_tokens_core = get_tokens(target_machine, remove_stops=True)
    if not target_tokens_core:
        target_tokens_core = get_tokens(target_machine, remove_stops=False)
        
    listing_tokens = get_tokens(listing_title, remove_stops=False)

    # If target has core tokens, check if all or sufficient core tokens match listing tokens
    if target_tokens_core:
        matched_count = sum(1 for t_token in target_tokens_core if fuzzy_token_match(t_token, listing_tokens))
        if matched_count == len(target_tokens_core) or (len(target_tokens_core) >= 3 and matched_count / len(target_tokens_core) >= 0.8):
            return True

    # Sliding window for ordered token sequence match
    if target_tokens_core and len(target_tokens_core) <= len(listing_tokens):
        k = len(target_tokens_core)
        for i in range(len(listing_tokens) - k + 1):
            window = listing_tokens[i:i+k]
            window_matched = all(fuzzy_token_match(t_token, [w_token]) for t_token, w_token in zip(target_tokens_core, window))
            if window_matched:
                return True

    return False

def find_matching_machine(listing_title, target_machines):
    for machine in target_machines:
        if is_machine_match(machine, listing_title):
            return machine
    return None
