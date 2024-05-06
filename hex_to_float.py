def hex_to_float(hex_str):
    # Convertir la représentation hexadécimale en entier signé sur 32 bits
    int_val = int(hex_str, 16)
    if int_val & 0x80000000:  # Vérifier si le bit de signe est à 1
        int_val = -(0x100000000 - int_val)  # Convertir en entier signé

    # Convertir l'entier signé en nombre flottant
    float_num = int_val / (1 << 24)  # Diviser par 2^24 car la partie fractionnaire est sur 24 bits

    return float_num

def main():
    # Demander à l'utilisateur d'entrer une représentation hexadécimale d'un nombre en virgule fixe
    hex_str = input("Entrez la représentation hexadécimale d'un nombre en virgule fixe (signed) : ")

    # Convertir la représentation hexadécimale en nombre flottant
    float_num = hex_to_float(hex_str)

    # Afficher le résultat
    print("Nombre flottant correspondant :", float_num)

if __name__ == "__main__":
    main()
# exemple :
# Entrez la représentation hexadécimale d'un nombre en virgule fixe (signed) : FF0001A0
# Nombre flottant correspondant : -0.9999752044677734