import re

def Id_gen(item_code, description, amount, dealer_id):
    # Convert description to uppercase for uniformity
    description = description.upper()

    # Define excluded words and brand replacements
    exclude_words = {"BICYCLE", "CYCLE", "BARHT", "NEW"}
    brand_replacements = {
        "HERCULES": "TI",
        "HERO": "HR",
        "HANKEY": "HY",
        "NEELAM": "NL",
    }

    # Replace brand names with abbreviations
    for brand, abbreviation in brand_replacements.items():
        description = description.replace(brand, abbreviation)

    # Remove excluded words
    description = " ".join(word for word in description.split() if word not in exclude_words)

    # Remove numbers and trailing words associated with them
    description = re.sub(r'\b\d+\s*\w*', '', description)

    # Remove any remaining digits and extra spaces
    description = re.sub(r'\d+', '', description).strip()

    # Take up to 4 initials from the first 4 words
    initials = "".join(word[0] for word in description.split()[:4])

    # Construct the ID
    return f"{item_code}{initials}{amount}{dealer_id[:4]}"

# # Example usage
# description = "Hercules Popular Cycle full stand"
# item_code = "CYSTD22"
# amount = 3900
# dealer_id = "TIVNS342"

# generated_id = generate_id(item_code, description, amount, dealer_id)
# print(generated_id)
def dealer_ID(strings, string1):
    # Remove digits and unwanted symbols from string, leaving only letters and spaces
    string_filtered = re.sub(r'[^a-zA-Z\s]', '', strings)
    
    # Take the first character of each word
    words = string_filtered.split()
    first_chars = ''.join([word[0] for word in words])
    
    # Take the last four characters from string1
    last_four_chars = string1[-4:]
    
    return first_chars[:4] + last_four_chars