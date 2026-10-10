"""
IL2.3: Estrategias de Planificación para Agentes LLM
==================================================

Este módulo explora diferentes estrategias de planificación para agentes LLM,
incluyendo planificación jerárquica, reactiva y orientada a objetivos.
"""

import time
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import heapq


class PlanningStrategy(Enum):
    """Tipos de estrategias de planificación"""
    HIERARCHICAL = "hierarchical"
    REACTIVE = "reactive"
    GOAL_ORIENTED = "goal_oriented"
    CONTINUOUS = "continuous"


@dataclass
class PlanStep:
    """Paso de un plan"""
    action: str
    description: str
    dependencies: List[str] = None
    estimated_duration: float = 1.0
    priority: int = 1
    status: str = "pending"
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class Plan:
    """Plan completo"""
    goal: str
    steps: List[PlanStep]
    created_at: float
    estimated_total_duration: float = 0.0
    status: str = "created"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
        self.estimated_total_duration = sum(step.estimated_duration for step in self.steps)


class Planner(ABC):
    """Planificador base"""
    
    def __init__(self, name: str):
        self.name = name
        self.plans: List[Plan] = []
        self.current_plan: Optional[Plan] = None
    
    @abstractmethod
    def create_plan(self, goal: str, context: Dict[str, Any]) -> Plan:
        """Crear un plan para lograr un objetivo"""
        pass
    
    @abstractmethod
    def execute_plan(self, plan: Plan) -> bool:
        """Ejecutar un plan"""
        pass
    
    def get_plan_status(self, plan: Plan) -> Dict[str, Any]:
        """Obtener estado de un plan"""
        completed_steps = sum(1 for step in plan.steps if step.status == "completed")
        return {
            "goal": plan.goal,
            "total_steps": len(plan.steps),
            "completed_steps": completed_steps,
            "progress": completed_steps / len(plan.steps) if plan.steps else 0,
            "status": plan.status
        }


class HierarchicalPlanner(Planner):
    """Planificador jerárquico"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.abstraction_levels = ["high", "medium", "low"]
    
    def create_plan(self, goal: str, context: Dict[str, Any]) -> Plan:
        """Crear plan jerárquico"""
        print(f"🎯 Creando plan jerárquico para: {goal}")
        
        # Descomponer objetivo en sub-objetivos
        sub_goals = self._decompose_goal(goal)
        
        # Crear pasos para cada nivel de abstracción
        steps = []
        for level in self.abstraction_levels:
            level_steps = self._create_level_steps(sub_goals, level)
            steps.extend(level_steps)
        
        plan = Plan(goal=goal, steps=steps)
        self.plans.append(plan)
        return plan
    
    def _decompose_goal(self, goal: str) -> List[str]:
        """Descomponer objetivo en sub-objetivos"""
        # Simulación de descomposición
        if "investigar" in goal.lower():
            return ["recopilar información", "analizar datos", "sintetizar resultados"]
        elif "desarrollar" in goal.lower():
            return ["diseñar", "implementar", "probar", "documentar"]
        else:
            return [goal]
    
    def _create_level_steps(self, sub_goals: List[str], level: str) -> List[PlanStep]:
        """Crear pasos para un nivel de abstracción"""
        steps = []
        for i, sub_goal in enumerate(sub_goals):
            step = PlanStep(
                action=f"{level}_level_action_{i}",
                description=f"Paso {level} para: {sub_goal}",
                priority=len(self.abstraction_levels) - self.abstraction_levels.index(level)
            )
            steps.append(step)
        return steps
    
    def execute_plan(self, plan: Plan) -> bool:
        """Ejecutar plan jerárquico"""
        print(f"🚀 Ejecutando plan jerárquico: {plan.goal}")
        
        # Ejecutar pasos en orden de prioridad
        sorted_steps = sorted(plan.steps, key=lambda x: x.priority, reverse=True)
        
        for step in sorted_steps:
            print(f"  📝 Ejecutando: {step.description}")
            step.status = "completed"
            time.sleep(0.1)  # Simular ejecución
        
        plan.status = "completed"
        return True


class ReactivePlanner(Planner):
    """Planificador reactivo"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.rules: List[Callable] = []
        self.current_state: Dict[str, Any] = {}
    
    def add_rule(self, condition: Callable, action: Callable):
        """Agregar regla reactiva"""
        def rule(state: Dict[str, Any]) -> Optional[str]:
            if condition(state):
                return action(state)
            return None
        self.rules.append(rule)
    
    def create_plan(self, goal: str, context: Dict[str, Any]) -> Plan:
        """Crear plan reactivo (simple)"""
        print(f"⚡ Creando plan reactivo para: {goal}")
        
        # Plan reactivo simple
        steps = [
            PlanStep(
                action="observe_environment",
                description="Observar el entorno actual",
                priority=1
            ),
            PlanStep(
                action="select_response",
                description="Seleccionar respuesta apropiada",
                priority=2
            ),
            PlanStep(
                action="execute_action",
                description="Ejecutar acción seleccionada",
                priority=3
            )
        ]
        
        plan = Plan(goal=goal, steps=steps)
        self.plans.append(plan)
        return plan
    
    def execute_plan(self, plan: Plan) -> bool:
        """Ejecutar plan reactivo"""
        print(f"⚡ Ejecutando plan reactivo: {plan.goal}")
        
        for step in plan.steps:
            print(f"  🔄 Ejecutando: {step.description}")
            
            # Aplicar reglas reactivas
            for rule in self.rules:
                result = rule(self.current_state)
                if result:
                    print(f"    Regla activada: {result}")
            
            step.status = "completed"
            time.sleep(0.1)
        
        plan.status = "completed"
        return True
    
    def update_state(self, new_state: Dict[str, Any]):
        """Actualizar estado del entorno"""
        self.current_state.update(new_state)


class GoalOrientedPlanner(Planner):
    """Planificador orientado a objetivos"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.goals: List[str] = []
        self.preconditions: Dict[str, List[str]] = {}
        self.effects: Dict[str, List[str]] = {}
    
    def add_action(self, action: str, preconditions: List[str], effects: List[str]):
        """Agregar acción con precondiciones y efectos"""
        self.preconditions[action] = preconditions
        self.effects[action] = effects
    
    def create_plan(self, goal: str, context: Dict[str, Any]) -> Plan:
        """Crear plan orientado a objetivos"""
        print(f"🎯 Creando plan orientado a objetivos para: {goal}")
        
        # Algoritmo de planificación hacia atrás
        steps = self._backward_planning(goal, context)
        
        plan = Plan(goal=goal, steps=steps)
        self.plans.append(plan)
        return plan
    
    def _backward_planning(self, goal: str, current_state: Dict[str, Any]) -> List[PlanStep]:
        """Planificación hacia atrás"""
        steps = []
        remaining_goals = [goal]
        achieved = set(current_state.keys())
        
        while remaining_goals:
            current_goal = remaining_goals.pop(0)
            
            if current_goal in achieved:
                continue
            
            # Encontrar acción que logre el objetivo
            action = self._find_action_for_goal(current_goal)
            if action:
                step = PlanStep(
                    action=action,
                    description=f"Ejecutar {action} para lograr {current_goal}",
                    dependencies=self.preconditions.get(action, [])
                )
                steps.append(step)
                
                # Agregar precondiciones como nuevos objetivos
                for precond in self.preconditions.get(action, []):
                    if precond not in achieved:
                        remaining_goals.append(precond)
                
                # Marcar efectos como logrados
                for effect in self.effects.get(action, []):
                    achieved.add(effect)
            else:
                print(f"⚠️ No se encontró acción para lograr: {current_goal}")
        
        return list(reversed(steps))  # Invertir para orden correcto
    
    def _find_action_for_goal(self, goal: str) -> Optional[str]:
        """Encontrar acción que logre un objetivo"""
        for action, effects in self.effects.items():
            if goal in effects:
                return action
        return None
    
    def execute_plan(self, plan: Plan) -> bool:
        """Ejecutar plan orientado a objetivos"""
        print(f"🎯 Ejecutando plan orientado a objetivos: {plan.goal}")
        
        for step in plan.steps:
            print(f"  🎯 Ejecutando: {step.description}")
            
            # Verificar precondiciones
            if step.dependencies:
                print(f"    Verificando precondiciones: {step.dependencies}")
            
            step.status = "completed"
            time.sleep(0.1)
        
        plan.status = "completed"
        return True


def demo_planning_strategies():
    """Demostración de estrategias de planificación"""
    print("🧠 DEMOSTRACIÓN: Estrategias de Planificación")
    print("=" * 50)
    
    # 1. Planificador Jerárquico
    print("\n1️⃣ Planificador Jerárquico:")
    hierarchical = HierarchicalPlanner("hierarchical_planner")
    plan1 = hierarchical.create_plan("Investigar inteligencia artificial", {})
    hierarchical.execute_plan(plan1)
    
    # 2. Planificador Reactivo
    print("\n2️⃣ Planificador Reactivo:")
    reactive = ReactivePlanner("reactive_planner")
    
    # Agregar reglas reactivas
    def high_temperature_condition(state):
        return state.get("temperature", 0) > 30
    
    def high_temperature_action(state):
        return "Activar sistema de refrigeración"
    
    reactive.add_rule(high_temperature_condition, high_temperature_action)
    reactive.update_state({"temperature": 35})
    
    plan2 = reactive.create_plan("Responder a cambios del entorno", {})
    reactive.execute_plan(plan2)
    
    # 3. Planificador Orientado a Objetivos
    print("\n3️⃣ Planificador Orientado a Objetivos:")
    goal_oriented = GoalOrientedPlanner("goal_oriented_planner")
    
    # Definir acciones
    goal_oriented.add_action(
        "investigar_ia",
        preconditions=["tener_internet", "tener_tiempo"],
        effects=["conocimiento_ia"]
    )
    goal_oriented.add_action(
        "conectar_internet",
        preconditions=[],
        effects=["tener_internet"]
    )
    goal_oriented.add_action(
        "reservar_tiempo",
        preconditions=[],
        effects=["tener_tiempo"]
    )
    
    plan3 = goal_oriented.create_plan("conocimiento_ia", {})
    goal_oriented.execute_plan(plan3)


def compare_planning_strategies():
    """Comparar estrategias de planificación"""
    print("\n📊 COMPARACIÓN DE ESTRATEGIAS")
    print("=" * 50)
    
    comparison = {
        "Jerárquica": {
            "Ventajas": "Estructura clara, escalable",
            "Desventajas": "Puede ser rígida",
            "Casos de uso": "Proyectos complejos, planificación a largo plazo"
        },
        "Reactiva": {
            "Ventajas": "Flexible, responde rápidamente",
            "Desventajas": "Puede ser impredecible",
            "Casos de uso": "Entornos dinámicos, respuestas inmediatas"
        },
        "Orientada a Objetivos": {
            "Ventajas": "Lógica clara, optimizada",
            "Desventajas": "Complejidad computacional",
            "Casos de uso": "Optimización, planificación eficiente"
        }
    }
    
    for strategy, info in comparison.items():
        print(f"\n🧠 {strategy}:")
        for key, value in info.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    demo_planning_strategies()
    compare_planning_strategies() 