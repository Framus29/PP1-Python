from typing import Annotated
from pydantic import Field

# Modularizar los tipos personalizados (Type Aliases)
# La nomenclatura recomendada es PascalCase

IntPositivo = Annotated[int, Field(gt=0, description="Debe ser mayor a 0")]
StrCortito = Annotated[str, Field(min_length=1, max_length=100)]
PrecioFloat = Annotated[float, Field(gt=0, description="Precio mayor a 0")]
