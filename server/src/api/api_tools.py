from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.features.build_insert_tag import insert_tags
from src.features.build_convert_output_of_model_to_xml import convert_to_ner_format
from src.models.predict_model import predict
from src.configs import LOG_DIR
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/api_tools.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@router.post("/preprocessing_tool")
async def preprocessing_tool(data: dict):
     try:
          if data is None:
               raise HTTPException(status_code=400, detail="Data not found")
          if "texts" not in data:
               raise HTTPException(status_code=400, detail="Missing 'texts' in request body.")
          if not data["texts"]:
               raise HTTPException(status_code=400, detail="Empty 'texts' in request body.")
          
          result = []
          for text in data["texts"]:               
               text, tags = predict(text)
               print(text, tags)
               result.append(convert_to_ner_format(text, tags))
          
          return JSONResponse(content={"status": "success", "data": result})
     except HTTPException as e:
          logger.error(f"HTTPException: {e.detail}")
          raise e
     except Exception as e:
          logger.error(f"Exception: {str(e)}")
          raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/annotation_tool")
async def annotation_tool(data: dict):
     try:
          if data is None:
               raise HTTPException(status_code=400, detail="Data not found")
          
          if "text" not in data:
               raise HTTPException(status_code=400, detail="Missing 'text' in request body.")
          
          if "tags" not in data:
               raise HTTPException(status_code=400, detail="Missing 'tags' in request body.")
          
          if not data["text"]:
               raise HTTPException(status_code=400, detail="Empty 'text' in request body.")
          
          if not data["tags"]:
               raise HTTPException(status_code=400, detail="Empty 'tags' in request body.")
          

          text = data["text"].get("sentences")
          tags = data["tags"]  
          print(text, tags)        
                    
          result = insert_tags({"text": text, "tags": tags})
          print(result)
          return JSONResponse(content={"status": "success", "data": result})
     except HTTPException as e:
          logger.error(f"HTTPException: {e.detail}")
          raise e
     except Exception as e:
          logger.error(f"Exception: {str(e)}")
          raise HTTPException(status_code=500, detail="Internal Server Error")
