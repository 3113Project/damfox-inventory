import { expect, test } from "vitest"
import { apiErrorMessage } from "./api"

test("maps catalog API errors to understandable messages", () => {
  expect(apiErrorMessage(404, "Product 9 not found")).toBe("La risorsa richiesta non esiste più.")
  expect(apiErrorMessage(409, "SKU already exists")).toBe("SKU already exists")
  expect(apiErrorMessage(422, [
    { loc: ["body", "name"], msg: "Field required" },
    { loc: ["body", "unit_of_measure_id"], msg: "Field required" },
  ])).toBe("Controlla i dati inseriti: Field required; Field required")
})
