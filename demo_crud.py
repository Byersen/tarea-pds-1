from user_model import UserRepository

def main():
    print("=== DEMOSTRACIÓN DEL CRUD DE USUARIOS ===\n")
    repo = UserRepository()

    print("1. CREAR USUARIOS")
    users = [
        repo.create("Ana Garcia", "ana@email.com", 28),
        repo.create("Luis Rodriguez", "luis@email.com", 35),
        repo.create("Maria Lopez", "maria@email.com", 22),
    ]
    for user in users:
        print(f"✓ Creado: {user.name} ({user.email}) - Edad: {user.age}")

    print("\n2. LEER USUARIO")
    user = repo.read(users[0].id)
    print(f"✓ Usuario leído: {user.name}")

    print("\n3. ACTUALIZAR USUARIO")
    updated = repo.update(users[1].id, name="Luis Rodriguez", age=36)
    print(f"✓ Actualizado: {updated.name} - Edad: {updated.age}")

    print("\n4. ELIMINAR USUARIO")
    repo.delete(users[2].id)
    print("✓ Usuario eliminado")

    print("\n5. VALIDACIONES DE DATOS")
    invalid_cases = [
        ("", "test@email.com", 25, "Nombre vacio"),
        ("Juan", "email-sin-arroba", 25, "Email invalido"),
        ("Pedro", "pedro@email.com", -5, "Edad negativa"),
        ("Ana", "ana@email.com", 200, "Edad muy alta"),
    ]

    for name, email, age, desc in invalid_cases:
        try:
            repo.create(name, email, age)
            print(f"✗ {desc}: deberia fallar")
        except ValueError as e:
            print(f"✓ {desc}: {e}")

    print(f"\nTotal final: {len(repo.list_all())}")

def demonstrate_property_concept():
    print("\n=== QUE SON LAS PROPIEDADES? ===")
    print("En lugar de probar casos especificos, se prueban PROPIEDADES.")
    print("Ejemplo:")
    print(" - Para cualquier nombre, email y edad validos:")
    print("   * El usuario creado debe poder leerse")
    print("   * Los datos deben conservarse exactamente")
    print("   * El ID debe ser unico y valido")

if __name__ == "__main__":
    main()
    demonstrate_property_concept()
