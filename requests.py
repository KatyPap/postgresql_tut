from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import List, Optional

app = FastAPI()

# Database configuration
DB_CONFIG = {
    "dbname": "your_database",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

class TableSchema(BaseModel):
    table_name: str
    columns: List[dict]  # [{"name": "id", "type": "INTEGER", "constraints": "PRIMARY KEY"}, ...]

class InsertData(BaseModel):
    table_name: str
    values: dict  # {"column1": "value1", "column2": "value2"}

@app.post("/create-table")
async def create_table(schema: TableSchema):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Construct CREATE TABLE query
        columns = [f"{col['name']} {col['type']} {col.get('constraints', '')}" 
                  for col in schema.columns]
        query = f"CREATE TABLE {schema.table_name} ({', '.join(columns)})"
        
        cur.execute(query)
        return {"message": f"Table {schema.table_name} created successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/insert/{table_name}")
async def insert_data(table_name: str, data: InsertData):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        columns = ', '.join(data.values.keys())
        values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) 
                          for v in data.values.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        
        cur.execute(query)
        conn.commit()
        return {"message": "Data inserted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/{table_name}/{id}")
async def delete_row(table_name: str, id: int):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        query = f"DELETE FROM {table_name} WHERE id = {id}"
        cur.execute(query)
        conn.commit()
        
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Row not found")
        
        return {"message": f"Row {id} deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/{table_name}")
async def select_all(table_name: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        query = f"SELECT * FROM {table_name}"
        cur.execute(query)
        rows = cur.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in cur.description]
        
        # Convert to list of dictionaries
        result = [dict(zip(columns, row)) for row in rows]
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)