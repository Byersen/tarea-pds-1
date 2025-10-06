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

    print(f"\nTotal final: {len(repo.list_all())}")

if __name__ == "__main__":
    main()
