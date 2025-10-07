from user_model import User, UserRepository


def main():
    """Demostración del funcionamiento del CRUD"""
    print("=== DEMOSTRACIÓN DEL CRUD DE USUARIOS ===\n")

    repo = UserRepository()

    print("1. CREAR USUARIOS")
    print("-" * 40)

    users = [
        repo.create("Ana Garcia", "ana@email.com", 28),
        repo.create("Luis Rodriguez", "luis@email.com", 35),
        repo.create("Maria Lopez", "maria@email.com", 22),
    ]

    for user in users:
        print(f"✓ Creado: {user.name} ({user.email}) - Edad: {user.age}")

    print(f"\nTotal de usuarios: {len(repo.list_all())}")

    print("\n2. LEER USUARIOS")
    print("-" * 40)
    first_user_id = users[0].id
    read_user = repo.read(first_user_id)
    print(f"✓ Usuario leido: {read_user.name} - ID: {read_user.id[:8]}...")
    print(f"✗ Usuario inexistente: {repo.read('fake-id')}")

    print("\n3. ACTUALIZAR USUARIOS")
    print("-" * 40)
    original_name = users[1].name
    updated_user = repo.update(users[1].id, name="Luis Fernando Rodriguez", age=36)
    print(f"✓ Actualizado: '{original_name}' → '{updated_user.name}'")
    print(f"  Edad: {users[1].age} → {updated_user.age}")

    print("\n4. LISTAR TODOS LOS USUARIOS")
    print("-" * 40)
    for i, user in enumerate(repo.list_all(), 1):
        status = "Activo" if user.active else "Inactivo"
        print(f"{i}. {user.name} ({user.email}) - {user.age} años - {status}")

    print("\n5. ELIMINAR USUARIOS")
    print("-" * 40)
    user_to_delete = users[2]
    success = repo.delete(user_to_delete.id)
    print(f"✓ Eliminado: {user_to_delete.name} - Exito: {success}")

    print("\n6. VALIDACIONES DE DATOS")
    print("-" * 40)
    invalid_cases = [
        ("", "test@email.com", 25, "Nombre vacio"),
        ("Juan", "email-sin-arroba", 25, "Email invalido"),
        ("Pedro", "pedro@email.com", -5, "Edad negativa"),
        ("Ana", "ana@email.com", 200, "Edad muy alta"),
    ]
    for name, email, age, desc in invalid_cases:
        try:
            User("id", name, email, age)
            print(f"✗ {desc}: Debería haber fallado")
        except ValueError as e:
            print(f"✓ {desc}: {e}")

    print("\n=== PROPERTY-BASED TESTING ===")
    print("Para ejecutar las pruebas basadas en propiedades:")
    print("1. pip install hypothesis pytest")
    print("2. pytest test_user_properties.py -v")


def demonstrate_property_concept():
    """Demostrar el concepto de Property-Based Testing"""
    print("\n=== ¿QUÉ SON LAS PROPIEDADES? ===")
    print("\nProbamos PROPIEDADES que siempre deben cumplirse:")
    print("  - Para cualquier nombre, email y edad válidos:")
    print("    * El usuario creado debe poder leerse")
    print("    * Los datos deben conservarse exactamente")
    print("    * El ID debe ser único y válido")


if __name__ == "__main__":
    main()
    demonstrate_property_concept()
