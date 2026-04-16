import json
import os
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
app = FastAPI(
	title="Talent Tracker API",
	description="API para gestión de talento.",
	version="1.0.0"
)

# Ahora la ruta base es /, porque el montaje en main.py la pone en /tracker/api/v1
@app.get("/")
def get_tracker_v1():
	return {"message": "Talent Tracker API v1 funcionando"}




@app.get("/records")
def get_records(
	status: str = Query(None, description="Filter by status: received, in_progress, selected, discarded"),
	stage: str = Query(None, description="Filter by stage: pending, review, personal_interview, technical_interview, offer_presented"),
	search: str = Query(None, description="Search in full_name or email"),
	page: int = Query(1, ge=1, description="Page number, default 1"),
	limit: int = Query(20, ge=1, le=100, description="Results per page, default 20")
):
	data_path = os.path.join(os.path.dirname(__file__), "data", "mock_data.json")
	try:
		with open(data_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		records = data.get("records", [])

		# Filtros
		if status:
			records = [r for r in records if r.get("status") == status]
		if stage:
			records = [r for r in records if r.get("stage") == stage]
		if search:
			search_lower = search.lower()
			records = [r for r in records if search_lower in r.get("full_name", "").lower() or search_lower in r.get("email", "").lower()]

		# Paginación
		total = len(records)
		start = (page - 1) * limit
		end = start + limit
		paginated = records[start:end]

		return {
			"total": total,
			"page": page,
			"limit": limit,
			"data": paginated
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error leyendo mock_data.json: {e}")
	


# Endpoint para obtener el detalle de un registro por id



@app.get("/records/{id}")
def get_record_by_id(id: str = Path(..., description="ID del registro")):
	data_path = os.path.join(os.path.dirname(__file__), "data", "mock_data.json")
	try:
		with open(data_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		records = data.get("records", [])
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error leyendo mock_data.json: {e}")

	for record in records:
		if record.get("id") == id:
			# Solo los campos principales
			return {
				"id": record.get("id"),
				"full_name": record.get("full_name"),
				"email": record.get("email"),
				"phone": record.get("phone"),
				"position": record.get("position"),
				"linkedin_url": record.get("linkedin_url"),
				"cv_url": record.get("cv_url"),
				"status": record.get("status"),
				"stage": record.get("stage"),
				"experience_years": record.get("experience_years"),
				"notes_count": record.get("notes_count"),
				"applied_at": record.get("applied_at"),
				"updated_at": record.get("updated_at")
			}
	return JSONResponse(status_code=404, content={"error": "Record not found"})