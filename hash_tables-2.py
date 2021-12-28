import random
import sys
import argparse

class HashTable:
    def __init__(self, num_slots, cap_per_slot, occupancy, total_trials, hash_type):
        self.num_slots = num_slots
        self.cap_per_slot = cap_per_slot
        self.occupancy = occupancy
        self.total_trials = total_trials
        self.hash_type = hash_type

        self.num_elements = int(occupancy * num_slots * cap_per_slot)
        self.trials_with_collisions = 0

    def run_hash_table(self):
        self.trials_with_collisions = 0
        for seed in range(self.total_trials):
            random.seed(seed)
            occupancy_at_slot = [0] * self.num_slots
            for i in range(self.num_elements):
                if self.hash_type == "standard":
                    slot_number = self.standard_hashing(occupancy_at_slot)
                elif self.hash_type == "2choice":
                    slot_number = self.two_choice_hashing(occupancy_at_slot)
                elif self.hash_type == "2left":
                    slot_number = self.two_left_hashing(occupancy_at_slot)
                occupancy_at_slot[slot_number] += 1
            
            if any([counter > self.cap_per_slot for counter in occupancy_at_slot]):
                self.trials_with_collisions += 1

        trials_did_not_exceed = 1.0 - (self.trials_with_collisions/self.total_trials)
        print("Fraction of trials in which slot size did not exceed capacity ", trials_did_not_exceed)
        return trials_did_not_exceed


    def standard_hashing(self, occupancy_at_slot):
        #TODO: Implement standard hashing by picking a slot number randomly between 0 and NUM_SLOTS - 1
        
        # Set variable rand_num to random integer
        rand_num = random.randint(0, self.num_slots -1)
        
        #TODO: Return the final slot number that you pick.
        return rand_num

    def two_choice_hashing(self, occupancy_at_slot):
        #TODO: Implement 2 choice hashing: pick two slot numbers randomly and then pick the less occupied of the 2
        # Break ties randomly.

        # Set random integers to variables
        rand_num1 = random.randint(0, self.num_slots -1)
        rand_num2 = random.randint(0, self.num_slots -1)
        # If value at random number less, then set return value to lesser one  
        if occupancy_at_slot[rand_num1] < occupancy_at_slot[rand_num2]:
            rand_num = rand_num1
        elif occupancy_at_slot[rand_num2] < occupancy_at_slot[rand_num1]:
            rand_num = rand_num2
        else:
            rand_num = random.choice([rand_num1, rand_num2])
       
        # Return the final slot number that you pick.
        return rand_num

    def two_left_hashing(self, occupancy_at_slot):
        #TODO: Implement 2 left hashing: pick two slots numbers from two sub tables and pick the less occupied of the 2
        # Always break ties towards one sub table

        # Set variable split_half to the number of slots divided by 2
        split_half = self.num_slots/2
        # Set random integers to variables
        rand_num1 = random.randint(0, split_half-1)
        rand_num2 = random.randint(split_half, self.num_slots -1)
        # If value at random number less, then set return value to lesser one  
        if occupancy_at_slot[rand_num1] < occupancy_at_slot[rand_num2]:
            rand_num = rand_num1
        elif occupancy_at_slot[rand_num2] < occupancy_at_slot[rand_num1]:
            rand_num = rand_num2
        else:
            rand_num = rand_num2
        
        # Return the final slot number that you pick.
        return rand_num

def check_hash_type(hash_type):
    if hash_type not in ["standard", "2choice", "2left"]:
        raise argparse.ArgumentTypeError("In valid hash type.  Valid hash types include standard, 2choice, and 2left.")
    return hash_type

def main(args):
    if args.occupancy > 1:
        raise("Occupancy should be less than or equal to 1")

    ht = HashTable(100, 5, args.occupancy, 1000, args.hash_type)
    ht.run_hash_table()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A hash table.')
    parser.add_argument('--occupancy', type=float,
                        help='how occupied is the table')
    parser.add_argument('--hash_type', type=check_hash_type,
                        help='type of table:  standard, 2choice, 2left')

    arguments = parser.parse_args()
    main(arguments)


