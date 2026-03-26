from dtos.engine.listar.response import EngineConfigDTO
from dtos.engine.configurar.response import ConfigurarEngineResponse


def para_dto(model) -> EngineConfigDTO:
    return EngineConfigDTO(
        id=str(model.id),
        engine_tipo=model.engine_tipo,
        provider=model.provider,
        modelo=model.modelo,
        ativo=model.ativo,
    )


def para_configurar_response(model) -> ConfigurarEngineResponse:
    return ConfigurarEngineResponse(
        id=str(model.id),
        engine_tipo=model.engine_tipo,
        provider=model.provider,
        modelo=model.modelo,
        ativo=model.ativo,
    )
