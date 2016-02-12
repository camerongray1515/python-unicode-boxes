class Box():
    def __init__(self, max_width=-1):
        self.max_width = max_width
        self.rows = []
        self.divider_width = 3
        self.border_width = 2
        self.characters = {
            "top-left": "╔",
            "top-right": "╗",
            "horizontal": "═",
            "vertical": "║",
            "vertical-tee-right": "╠",
            "vertical-tee-left": "╣",
            "bottom-left": "╚",
            "bottom-right": "╝"
        }

    @property
    def width(self): # TODO: Fix this for fixed dividers
        box_width = 0
        for row in self.rows:
            row_width = 0
            if row["type"] == "row":
                for slot_num in row["value"].slot_contents:
                    row_width += len(row["value"].slot_contents[slot_num])
                row_width += self.divider_width * len(row["value"].dividers)
            elif row["type"] == "text":
                row_width += len(row["value"])
            if row_width > box_width:
                box_width = row_width
        box_width += self.border_width * 2
        return box_width

    def render(self):
        box_width = self.width
        output_string = ""
        # Top row
        output_string += (self.characters["top-left"]
            + self.characters["horizontal"] * (box_width - 2)
            + self.characters["top-right"] + "\n")

        for row in self.rows:
            output_string += self._render_row(row)

        # Bottom row
        output_string += (self.characters["bottom-left"]
            + self.characters["horizontal"] * (box_width - 2)
            + self.characters["bottom-right"] + "\n")
        print(output_string)

    def _render_row(self, row):
        row_type = row["type"]
        row_value = None if row_type == "divider" else row["value"]
        rendered = ""
        if row_type == "divider":
            rendered += self.characters["vertical-tee-right"]
        else:
            rendered += self.characters["vertical"] + " "

        if row_type == "text":
            rendered += row_value + " " * (
                self.width - len(row_value) - (self.border_width * 2))
        elif row_type == "divider":
            rendered += self.characters["horizontal"] * (self.width - 2)
        elif row_type == "row":
            for slot_num in row_value.slot_contents:
                slot_value = row_value.slot_contents[slot_num]
                rendered += slot_value
                if slot_num < (row_value.num_slots - 1):
                    rendered += " {} ".format(self.characters["vertical"])

        if row_type == "divider":
            rendered += self.characters["vertical-tee-left"]
        else:
            rendered += " " + self.characters["vertical"]

        rendered += "\n"

        return rendered

    def add_row(self, row):
        if type(row) == Row:
            self.rows.append({"type": "row", "value": row})
        else:
            self.rows.append({"type": "text", "value": str(row)})

    def add_divider(self):
        self.rows.append({"type": "divider"})

class Row():
    def __init__(self):
        self.num_slots = 1
        self.slot_contents = {0: ""}
        self.dividers = []

    def add_text(self, slot, text):
        try:
            self.slot_contents[slot] = text
        except KeyError:
            raise Exception("Slot does not exist")

    def add_divider(self, position=-1):
        divider = {
            "type": "fixed" if position >= 0 else "floating"
        }
        if divider["type"] == "fixed":
            dividier["position"] = position
        self.dividers.append(divider)
        self.num_slots += 1
        self.slot_contents[self.num_slots-1] = ""

if __name__ == "__main__":
    b = Box()
    b.add_row("Foo")
    b.add_divider()
    b.add_row("Foobar")
    b.add_row("Bar")
    b.add_divider()
    r = Row()
    r.add_divider()
    r.add_text(0, "foo")
    r.add_text(1, "bar")
    b.add_row(r)
    b.render()
