import pytest
from hypothesis import given, strategies as st, assume
from user_model import User, UserRepository


# Estrategias para generar datos de prueba
valid_names = st.text(min_size=1, max_size=50).filter(lambda x: x.strip())
valid_emails = st.emails()
valid_ages = st.integers(min_value=0, max_value=150)
booleans = st.booleans()


class TestUserPropertyBased:
    """Pruebas basadas en propiedades para el modelo User y UserRepository"""
    
    def setup_method(self):
        """Configurar un repositorio limpio para cada prueba"""
        self.repo = UserRepository()
        # Asegurar que el repositorio esté completamente vacío
        self.repo.clear()
    
    @given(name=valid_names, email=valid_emails, age=valid_ages, active=booleans)
    def test_create_user_property(self, name, email, age, active):
        """
        Property: Un usuario creado debe existir en el repositorio 
        y conservar todas sus propiedades originales
        """
        # Acción: crear usuario
        user = self.repo.create(name, email, age, active)
        
        # Propiedades que deben cumplirse:
        # 1. El usuario debe tener un ID válido
        assert user.id is not None
        assert len(user.id) > 0
        
        # 2. Las propiedades deben conservarse
        assert user.name == name
        assert user.email == email
        assert user.age == age
        assert user.active == active
        
        # 3. El usuario debe existir en el repositorio
        retrieved_user = self.repo.read(user.id)
        assert retrieved_user is not None
        assert retrieved_user == user
    
    @given(name=valid_names, email=valid_emails, age=valid_ages, active=booleans)
    def test_read_after_create_property(self, name, email, age, active):
        """
        Property: Después de crear un usuario, 
        siempre debe ser posible leerlo con el mismo ID
        """
        # Crear usuario
        created_user = self.repo.create(name, email, age, active)
        
        # Leer usuario
        read_user = self.repo.read(created_user.id)
        
        # Property: el usuario leído debe ser idéntico al creado
        assert read_user is not None
        assert read_user.id == created_user.id
        assert read_user.name == created_user.name
        assert read_user.email == created_user.email
        assert read_user.age == created_user.age
        assert read_user.active == created_user.active
    
    @given(name=valid_names, email=valid_emails, age=valid_ages, 
           new_name=valid_names, new_email=valid_emails, new_age=valid_ages)
    def test_update_user_property(self, name, email, age, new_name, new_email, new_age):
        """
        Property: Actualizar un usuario debe cambiar solo los campos especificados
        y el usuario debe seguir siendo legible
        """
        # Crear usuario inicial
        user = self.repo.create(name, email, age, True)
        original_id = user.id
        
        # Actualizar usuario
        updated_user = self.repo.update(user.id, name=new_name, email=new_email, age=new_age)
        
        # Properties:
        # 1. La actualización debe ser exitosa
        assert updated_user is not None
        
        # 2. El ID no debe cambiar
        assert updated_user.id == original_id
        
        # 3. Los campos actualizados deben tener los nuevos valores
        assert updated_user.name == new_name
        assert updated_user.email == new_email
        assert updated_user.age == new_age
        
        # 4. El campo no actualizado (active) debe conservar su valor
        assert updated_user.active == True
        
        # 5. El usuario actualizado debe ser legible desde el repositorio
        read_user = self.repo.read(user.id)
        assert read_user == updated_user
    
    @given(name=valid_names, email=valid_emails, age=valid_ages, active=booleans)
    def test_delete_user_property(self, name, email, age, active):
        """
        Property: Después de eliminar un usuario, 
        no debe ser posible leerlo y el conteo debe decrementar
        """
        # Contar usuarios iniciales
        initial_count = len(self.repo.list_all())
        
        # Crear usuario
        user = self.repo.create(name, email, age, active)
        user_id = user.id
        
        # Verificar que existe
        assert self.repo.read(user_id) is not None
        assert len(self.repo.list_all()) == initial_count + 1
        
        # Eliminar usuario
        delete_result = self.repo.delete(user_id)
        
        # Properties:
        # 1. La eliminación debe ser exitosa
        assert delete_result == True
        
        # 2. El usuario no debe ser legible después de eliminarlo
        assert self.repo.read(user_id) is None
        
        # 3. El conteo de usuarios debe decrementar
        assert len(self.repo.list_all()) == initial_count
    
    @given(st.lists(st.tuples(valid_names, valid_emails, valid_ages, booleans), 
                    min_size=0, max_size=20))
    def test_list_all_property(self, users_data):
        """
        Property: list_all() debe devolver exactamente todos los usuarios creados
        """
        # Limpiar repositorio al inicio del test para asegurar estado limpio
        self.repo.clear()
        
        created_users = []
        
        # Crear todos los usuarios
        for name, email, age, active in users_data:
            user = self.repo.create(name, email, age, active)
            created_users.append(user)
        
        # Obtener lista completa
        all_users = self.repo.list_all()
        
        # Properties:
        # 1. El número de usuarios debe coincidir
        assert len(all_users) == len(created_users)
        
        # 2. Todos los usuarios creados deben estar en la lista
        created_ids = {user.id for user in created_users}
        listed_ids = {user.id for user in all_users}
        assert created_ids == listed_ids
    
    def test_read_nonexistent_user_property(self):
        """
        Property: Intentar leer un usuario inexistente debe devolver None
        """
        # IDs que no existen
        fake_ids = ["fake-id", "123456", "", "nonexistent"]
        
        for fake_id in fake_ids:
            result = self.repo.read(fake_id)
            assert result is None
    
    def test_update_nonexistent_user_property(self):
        """
        Property: Intentar actualizar un usuario inexistente debe devolver None
        """
        result = self.repo.update("fake-id", name="New Name")
        assert result is None
    
    def test_delete_nonexistent_user_property(self):
        """
        Property: Intentar eliminar un usuario inexistente debe devolver False
        """
        result = self.repo.delete("fake-id")
        assert result == False


# Pruebas de validación de datos
class TestUserValidationProperties:
    """Pruebas de propiedades para validación de datos"""
    
    @given(st.text().filter(lambda x: not x.strip()))  # Nombres vacíos o solo espacios
    def test_empty_name_raises_error_property(self, invalid_name):
        """Property: Los nombres vacíos deben lanzar ValueError"""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User("id", invalid_name, "test@example.com", 25)
    
    @given(st.text().filter(lambda x: "@" not in x or not x.strip()))  # Emails inválidos
    def test_invalid_email_raises_error_property(self, invalid_email):
        """Property: Los emails inválidos deben lanzar ValueError"""
        assume(invalid_email.strip())  # Evitar nombres vacíos para enfocar en email
        
        with pytest.raises(ValueError, match="Invalid email format"):
            User("id", "Valid Name", invalid_email, 25)
    
    @given(st.integers().filter(lambda x: x < 0 or x > 150))  # Edades inválidas
    def test_invalid_age_raises_error_property(self, invalid_age):
        """Property: Las edades fuera del rango válido deben lanzar ValueError"""
        with pytest.raises(ValueError, match="Age must be between 0 and 150"):
            User("id", "Valid Name", "test@example.com", invalid_age)


if __name__ == "__main__":
    # Ejecutar algunas pruebas de ejemplo
    print("Ejecutando pruebas básicas del CRUD...")
    
    repo = UserRepository()
    
    # Crear
    user = repo.create("Juan Pérez", "juan@example.com", 30)
    print(f"Usuario creado: {user}")
    
    # Leer
    read_user = repo.read(user.id)
    print(f"Usuario leído: {read_user}")
    
    # Actualizar
    updated_user = repo.update(user.id, name="Juan Carlos Pérez", age=31)
    print(f"Usuario actualizado: {updated_user}")
    
    # Listar
    all_users = repo.list_all()
    print(f"Todos los usuarios: {all_users}")
    
    # Eliminar
    deleted = repo.delete(user.id)
    print(f"Usuario eliminado: {deleted}")
    
    print("\nPara ejecutar las pruebas basadas en propiedades:")
    print("pip install hypothesis pytest")
    print("pytest test_user_properties.py -v")