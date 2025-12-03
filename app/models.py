from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Input(Base):
    __tablename__ = "inputs"

    id_input = Column(Integer, primary_key=True, index=True)
    timestamp_input = Column(TIMESTAMP)
    employee_id = Column(Integer)
    age = Column(Integer)
    outputs = relationship("Output", back_populates="input")

class Output(Base):
    __tablename__ = "outputs"

    id_output = Column(Integer, primary_key=True, index=True)
    id_input = Column(Integer, ForeignKey("inputs.id_input"))
    prediction = Column(Integer)
    probability = Column(Float)

    input = relationship("Input", back_populates="outputs")
