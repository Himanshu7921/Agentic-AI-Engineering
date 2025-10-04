# **Planning Pattern**

## **1. What Planning Is**

* Planning = **figuring out the steps to reach a goal**.
* Unlike reactive agents (Prompt Chaining, Tool Use), a planning agent **thinks ahead**.
* Example:

  > Goal: “Organize a team offsite”
  > Planning agent figures out **what to do first, next, and last** to achieve this.

---

## **2. How Planning Works**

1. **Current State** → The agent observes the present situation.

   * Example: Budget, dates, available venues.
2. **Goal State** → The agent knows the desired outcome.

   * Example: Team offsite successfully organized.
3. **Plan Generation** → The agent figures out a **sequence of steps** to move from current → goal state.

   * **Key point:** The plan is **not pre-defined**; the agent discovers the best actions dynamically.

---

## **3. Adaptability**

* Planning agents can handle **unexpected changes**.

  * Example: Venue booked? Caterer unavailable? The agent **adjusts the plan** to still reach the goal.
* **Contrast with fixed-task agents:** Fixed scripts fail if the environment changes.

---

## **4. When to Use Planning**

* Use planning when the **“how” is unknown, complex, or dynamic**.
* Avoid planning when tasks are **simple and repeatable** → fixed workflows are faster and safer.

---

## **5. TL;DR**

* **Planning** = “Figure out steps to reach a goal, and adjust them if needed.”
* Steps obvious → no planning needed.
* Steps complex/unpredictable → planning agent is essential.

---

## **6. Analogy**

| Fixed-task Agent       | Planning Agent                                                                |
| ---------------------- | ----------------------------------------------------------------------------- |
| Follows recipe exactly | Cooks dinner **without a recipe** – adapts based on ingredients and situation |

---

## **7. Real-World Examples**

### **Example 1 – Self-Driving Cars**

**Goal:** Reach office safely.
**Planning Steps:**

1. Check map for possible routes.
2. Decide the fastest or safest route.
3. Detect and avoid obstacles (cars, pedestrians, cones).
4. Adjust speed/lane changes per traffic rules.
5. Re-plan if traffic jams or accidents occur.

> The car **doesn’t move randomly** — it plans each action and adapts continuously.

### **Example 2 – Smart Assistants (Siri, Google Assistant)**

**Goal:** Book a flight.
**Planning Steps:**

1. Ask for departure/arrival details.
2. Check available flights.
3. Compare prices and times.
4. Confirm booking and send ticket.

> The assistant **follows a step-by-step plan** to complete a multi-step task efficiently.
