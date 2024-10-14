import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from items.routers import router as items
from clock_in.routers import router as clock_in


app = FastAPI(debug=True)

# Allow to access the api , * can create it publicly or for specified app have to add IP.
origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

# Add routes to the apps...
app.include_router(items)
app.include_router(clock_in)

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, host="0.0.0.0", port=8423)
