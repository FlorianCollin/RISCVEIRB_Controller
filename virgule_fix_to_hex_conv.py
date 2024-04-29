def float_to_bin_and_hex(float_num):
    # Conversion de la partie entière en binaire sur 8 bits
    integer_part = int(float_num)
    integer_part_bin = format(integer_part, '08b')

    # Conversion de la partie fractionnaire en binaire sur 24 bits
    fractional_part = float_num - integer_part
    fractional_part_bin = ''
    for _ in range(24):
        fractional_part *= 2
        bit = int(fractional_part)
        fractional_part_bin += str(bit)
        fractional_part -= bit

    # Conversion de la partie entière en hexadécimal
    integer_part_hex = hex(integer_part)[2:].zfill(2)  # [2:] pour supprimer '0x' et zfill pour obtenir toujours 2 caractères

    # Conversion de la partie fractionnaire en hexadécimal
    fractional_part_hex = hex(int(fractional_part_bin, 2))[2:].zfill(6)  # [2:] pour supprimer '0x' et zfill pour obtenir toujours 6 caractères

    # Concaténation de l'hexadécimal complet
    full_hex = integer_part_hex + fractional_part_hex

    return integer_part_bin, fractional_part_bin, full_hex

def main():
    # Demander à l'utilisateur d'entrer un nombre flottant
    float_num = float(input("Entrez un nombre flottant : "))

    # Convertir le flottant en binaire et en hexadécimal
    integer_part_bin, fractional_part_bin, full_hex = float_to_bin_and_hex(float_num)

    # Afficher les résultats
    print("Partie entière en binaire :", integer_part_bin)
    print("Partie fractionnaire en binaire :", fractional_part_bin)
    print("Hexadécimal complet :", full_hex)

if __name__ == "__main__":
    main()
