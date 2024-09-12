runDev:
	export LOCAL_IMAGE_GEN_API_KEY=secret-token && uvicorn app.server:app --reload
