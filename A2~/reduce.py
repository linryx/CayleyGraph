from sage.all import RootSystem

def reduce_by_one_step(matrix_or_type, input_word):
    print("=" * 60)
    print(f"Starting Scan for Word: {input_word}")
    print("=" * 60)
    
    root_system = RootSystem(matrix_or_type)
    root_space = root_system.root_space()
    reflections = root_space.simple_reflections()
    generator_keys = list(reflections.keys())
    
    # 1. Map simple root indices to immutable vector signatures
    simple_root_vectors = {}
    for i in generator_keys:
        v = root_space.simple_root(i).to_vector()
        v.set_immutable()  # Freeze vector to make it hashable
        simple_root_vectors[i] = v
    
    # 2. FIX: Generate Small Roots by converting them to immutable tuples
    # This completely eliminates the "unhashable" TypeError
    small_roots_signatures = set()
    queue = [root_space.simple_root(i) for i in generator_keys]
    visited_roots = set()
    
    while queue:
        current_root = queue.pop(0)
        v_raw = current_root.to_vector()
        v_sig = tuple(v_raw) # A standard Python tuple is always hashable!
        
        if v_sig in visited_roots:
            continue
        visited_roots.add(v_sig)
        
        # Geometrically isolate the true, bounded positive small root space
        if max(abs(c) for c in v_raw) <= 2:
            small_roots_signatures.add(v_sig)
            for i in generator_keys:
                next_root = reflections[i](current_root)
                queue.append(next_root)

    word_history = []   
    current_active_signatures = set() 
    
    # 3. Stream the word left-to-right through the verified mirror pool
    for current_step, next_letter in enumerate(input_word, start=1):
        alpha_b_sig = tuple(simple_root_vectors[next_letter])
        
        # --- THE BRINK-HOWLETT COLLISION TEST ---
        if alpha_b_sig in current_active_signatures:
            print(f"\n[COLLISION DETECTED] at Step {current_step} reading letter '{next_letter}'!")
            
            # Trace backward to locate the twin step marker
            step_x = None
            for past_idx in range(len(word_history) - 1, -1, -1):
                if word_history[past_idx] == next_letter:  
                    step_x = past_idx + 1
                    break
            
            print(f" -> Mathematical twin found in history at Step X = {step_x}")
            print(f" -> Activating Strong Exchange Property...")
            
            del word_history[step_x - 1]
            middle_letters = word_history[step_x - 1:]
            
            # --- THE GEOMETRIC TWIST (Conjugation) ---
            new_tail = []
            for y in middle_letters:
                root_y = root_space.simple_root(y)
                reflected_root_y_vec = reflections[next_letter](root_y).to_vector()
                reflected_root_y_vec.set_immutable()
                
                matched_generator = y
                for g_idx in generator_keys:
                    if simple_root_vectors[g_idx] == reflected_root_y_vec:
                        matched_generator = g_idx
                        break
                new_tail.append(matched_generator)
            
            intact_prefix = word_history[:step_x - 1]
            unread_letters = input_word[current_step:]
            partially_reduced_word = intact_prefix + new_tail + unread_letters
            
            print(f"\n[TERMINATING LOGIC TRIGGERED]")
            print(f"One-step reduction output: {partially_reduced_word}")
            print("=" * 60)
            return partially_reduced_word
            
        # --- SAFE STEP POOL UPDATES ---
        next_active_signatures = set()
        for sig in current_active_signatures:
            root_element = root_space.from_vector(vector(sig))
            reflected_sig = tuple(reflections[next_letter](root_element).to_vector())
            
            if reflected_sig in small_roots_signatures:
                next_active_signatures.add(reflected_sig)
                
        next_active_signatures.add(alpha_b_sig)
        word_history.append(next_letter)
        current_active_signatures = next_active_signatures
        print(f"Step {current_step}: Processing letter '{next_letter}' safely.")

    print("\n[SCAN COMPLETE] Word was already completely reduced.")
    return input_word

# Executing on the infinite Affine A2 group
affine_a2 = ['A', 2, 1]
messy_word = [0, 1, 2, 1, 0, 1, 2, 0]

output = reduce_by_one_step(affine_a2, messy_word)

