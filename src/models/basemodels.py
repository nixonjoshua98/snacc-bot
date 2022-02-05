from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        allow_population_by_field_name = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = kwargs.get("by_alias", True)

        return super().dict(**kwargs)