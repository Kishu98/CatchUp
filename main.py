def initialize_game(n):
    return set(range(1, n+1))

def get_valid_choices(available_number, last_sum, player_sum):

    valid_choices = []
    nums = list(available_number)

    total_subsets = 1 << len(nums)

    for i in range(1, total_subsets):
        subset = set()

        for j in range(len(nums)):
            if i & (1 << j):
                subset.add(nums[j])

                if sum(subset) + player_sum >= last_sum and subset not in valid_choices:
                    # print(f"{subset} sum is -> {sum(subset)}")
                    valid_choices.append(subset)
                    break
                elif subset in valid_choices:
                    break


    return valid_choices

def minimax(available_number, p1_sum, p2_sum, is_p2_turn, depth=0):
    if not available_number:  
        return p2_sum - p1_sum, None

    valid_choices = get_valid_choices(available_number, p1_sum if is_p2_turn else p2_sum, p2_sum if is_p2_turn else p1_sum)

    if not valid_choices:
        return p2_sum - p1_sum, None  

    if is_p2_turn:
        max_eval = float("-inf")
        best_move = None

        for choice in valid_choices:
            new_available = available_number - choice
            new_p2_sum = p2_sum + sum(choice)
            eval_score, _ = minimax(new_available, p1_sum, new_p2_sum, False, depth + 1)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = choice

        return max_eval, best_move

    else:
        min_eval = float("inf")
        best_move = None

        for choice in valid_choices:
            new_available = available_number - choice
            new_p1_sum = p1_sum + sum(choice)
            eval_score, _ = minimax(new_available, new_p1_sum, p2_sum, True, depth + 1)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = choice

        return min_eval, best_move

def player_turn(player, last_sum, player_sum, available_number, first_move):
    if first_move:
        valid_choices = list(available_number)
        print(f"Valid choices -> {valid_choices}\n")
        user_input = int(input(f"{player} select  "))

        # choosen_set = {random.choice(valid_choices)}
        choosen_set = {valid_choices[user_input-1]}
        first_move = False
    else:
        valid_choices = get_valid_choices(available_number, last_sum, player_sum)

        if not valid_choices:
            return None, first_move

        print(f"Valid choices -> {valid_choices}\n")

        if player == "P2":
            _, best_move = minimax(available_number, last_sum, player_sum, True)
            choosen_set = best_move
        else:
            user_input = int(input(f"{player} "))
            choosen_set = valid_choices[user_input-1]

    
    print(f"{player} chose -> {choosen_set}")
    available_number -= choosen_set

    return sum(choosen_set), first_move

def checkWinner(p1_sum, p2_sum):
    if p1_sum > p2_sum:
        return "P1 is the winner"
    elif p2_sum > p1_sum:
        return "P2 is the winner"
    else:
        return "It's a tie"

def play_game(n):
    print("Let's start the Catch-Up Game!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    available_number = initialize_game(n)
    
    p1_sum, p2_sum = 0, 0
    p1_turn = True
    first_move = True

    while available_number:
        if p1_turn:
            last_sum = p2_sum
            player_sum = p1_sum
            player = "P1"
        else:
            last_sum = p1_sum
            player_sum = p2_sum
            player = "P2"

        print(f"\n~~~~~Current Scores~~~~~\nP1 score -> {p1_sum} \nP2 score -> {p2_sum}\n")
        print(f"Available Numbers -> {available_number}\n")
        new_sum, first_move = player_turn(player, last_sum, player_sum, available_number, first_move)

        if new_sum is None:
            break

        if p1_turn:
            p1_sum += new_sum
        else:
            p2_sum += new_sum

        p1_turn = not p1_turn

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Final Scores: P1 = {p1_sum}, P2 = {p2_sum}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~ Winner ~~~~~~~~~~~~")
    print(checkWinner(p1_sum, p2_sum))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

n = int(input("Enter the maximum number -> "))
play_game(n)
