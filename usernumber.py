import random


def _get_counter_with_file(f, user_id: str) -> int:
	"""Get this user's counter from a file that stores counters. 0 if not found."""
	for line in f:
		searched_user_id, counter = line.split(" ")
		if searched_user_id == user_id:
			return int(counter)
	return 0


def generate(user_id: int) -> int:
	user_id = str(user_id)

	with open("usernumbers.csv", "a+") as f:
		# Find this user's information from a file
		counter = _get_counter_with_file(f, user_id)

		# User does not exist?
		if counter == 0:
			# Seek to the end of the file to write a new entry
			f.seek(0, 2)
		else:
			# Seek to the beginning of their entry to update it
			current_position = f.tell()
			length = len(user_id) + 1 + len(str(counter))
			new_position = current_position - length
			if new_position < 0:
				new_position = 0
			f.seek(new_position)

		# Generate this user's next number
		random.seed(user_id)
		for _ in range(counter):
			random.random()
		user_number = str(random.randint(0, 999))

		# Increment this user's counter so they will get
		#   the number after this one next time
		counter += 1

		# Write this user's entry with their new counter
		f.write(user_id + " " + str(counter))

		return user_number


def get_counter(user_id: int) -> int:
	user_id = str(user_id)
	try:
		with open("usernumbers.csv", "r") as f:
			return _get_counter_with_file(f, user_id)
	except FileNotFoundError:
		return 0
