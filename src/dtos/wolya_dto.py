from pydantic import BaseModel, Field


class WolyaDTO(BaseModel):
    amazon_url: str = Field(alias='amazonUrl')
    deal_id: str = Field(alias='dealId')
