from fastapi import FastAPI, HTTPException, status 
from pydantic import BaseModel 


app = FastAPI(title="Магазин Станков") 

class MachineCreate(BaseModel): 
    name: str
    manufacturer: str 
    model: str
    in_stock: bool  

class MachineUpdate(BaseModel): 
    name: str | None = None 
    manufacturer: str | None = None 
    model: str | None = None 
    in_stock: bool | None = None 


machines =  [
        { 
        "name": "p767", 
        "manufacturer": "Agrafon",  
        "model": "gtyh33", 
        "in_stock": True,
        "id": 1,
    },

    {   
        "name": "y784", 
        "manufacturer": "APrime", 
        "model": "hfgh5", 
        "in_stock": False,
        "id": 2, 
    }

        ] 

next_id = 3 


def find_machine(machine_id: int): 
    for item in machines: 
        if item["id"] == machine_id: 
            return item
    raise HTTPException(status_code=404, detail="Станок не был найден в каталоге")



@app.get("/machines")
async def get_machines(in_stock: bool | None = None,
                       manufacturer: str | None = None):   
        
        return [machine for machine in machines if (in_stock is None or in_stock == machine["in_stock"] ) and (manufacturer is None or manufacturer == machine["manufacturer"])]



@app.get("/machines/{machine_id}") 
async def get_machines_id(machine_id: int): 
    return find_machine(machine_id) 



@app.post("/machines", status_code=status.HTTP_201_CREATED)
async def create_machine(machine: MachineCreate):  
    new_machine = machine.model_dump()
    global next_id

    new_machine["id"] = next_id
    next_id += 1

    machines.append(new_machine) 

    return new_machine 



@app.put("/machines/{machine_id}") 
async def put_machine(machine_id: int, machine: MachineCreate): 
    data = machine.model_dump()

    item = find_machine(machine_id) 
    item.update(data) 

    return item       



@app.patch("/machines/{machine_id}") 
async def update_machine(machine_id: int, machine: MachineUpdate):
    data = machine.model_dump(exclude_unset=True) 

    item = find_machine(machine_id) 
    item.update(data) 

    return item



@app.delete("/machines/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_machine(machine_id: int):  

    item = find_machine(machine_id) 
    machines.remove(item) 