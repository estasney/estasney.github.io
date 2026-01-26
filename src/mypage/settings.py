from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_repo_root() -> Path:
    import importlib.resources

    app_dir = Path(importlib.resources.files("mypage"))  # pyright: ignore[reportArgumentType]
    if app_dir.parent.name == "src":
        return app_dir.parent.parent
    return app_dir


def get_repo_env_file() -> Path | None:
    # Handle .env located at repo root vs adjacent to config
    import importlib.resources

    app_dir = Path(importlib.resources.files("mypage"))  # pyright: ignore[reportArgumentType]
    if app_dir.parent.name == "src" and (env_file := app_dir.parent.parent / ".env").exists():
        return env_file
    if (env_file := app_dir / ".env").exists():
        return env_file
    return None

class Settings(BaseSettings):
    """Contact information loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_prefix="CONTACT_",
        extra="ignore",
        case_sensitive=False,
    )
    me_file: Path = Field(default_factory=lambda: get_repo_root() / "me.yml")
    repo_root: Path = Field(default_factory=get_repo_root)
    info: list[str] | None = Field(default=None)
    



@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings(_env_file=get_repo_env_file())  # pyright: ignore[reportCallIssue]
