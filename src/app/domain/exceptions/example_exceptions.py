class ExampleNotFoundError(Exception):
    def __init__(self, example_id: int) -> None:
        super().__init__(f"Example with id {example_id} not found")
        self.example_id = example_id

class ExampleAlreadyExistsError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Example with name '{name}' already exists")
        self.name = name
