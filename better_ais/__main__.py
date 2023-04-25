from . import (
    __author__,
    __version__,
    __built_at__,
    __commit_sha__,
    __branch__,
)
from better_ais.di import core_di
from better_ais.api.routes import api_router

app = core_di.app
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    await core_di.database


@app.get("/build_info")
async def build_info():
    return {
        "author": __author__,
        "version": __version__,
        "built_at": __built_at__,
        "commit_sha": __commit_sha__,
        "branch": __branch__,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
