import tkinter as tk
import json


class Game:
    def __init__(self, saved_game) -> None:
        self.read_save(saved_game)
        self.window = tk.Tk()
        self.window.title("IDLE Game")
        self.window.geometry("400x400")

        self.total = tk.Label(self.window, text=f"Total: {self.total_money}")
        self.cps_label = tk.Label(self.window, text=f"CPS: {self.total_cps}")
        self.clicker = tk.Button(
            self.window, text=f"+{self.click_value}", command=(lambda: self.add_total())
        )
        self.store_label = tk.Label(self.window, text="Store")

        self.total.pack()
        self.cps_label.pack()
        self.clicker.pack()
        self.store_label.pack()

        for item, lst in self.store.items():
            labels = (
                tk.Label(self.window, text=f"Cost: {lst[0]}"),
                tk.Label(self.window, text=f"CPS: {lst[1]}"),
                tk.Label(self.window, text=f"Owned: {lst[2]}"),
            )
            tk.Button(
                self.window,
                text=f"Buy {item}",
                command=(lambda item=item, labels=labels: self.buy_items(item, labels)),
            ).pack()
            for x in labels:
                x.pack()

        tk.Button(self.window, text="Save", command=self.autosave).pack()
        self.autosave()
        self.update_cps()
        self.window.mainloop()

    def add_total(self):
        self.total_money += 1
        self.total.config(text=f"Total: {self.total_money}")

    def buy_items(self, item, labels):
        cost = self.store[item][0]
        cps = self.store[item][1]
        owned = self.store[item][2]

        if self.total_money >= cost:
            # deduct cost from total
            self.total_money -= cost
            # add item cps to total cps
            self.total_cps += cps
            self.cps_label.config(text=f"CPS: {self.total_cps}")
            self.total.config(text=f"Total: {self.total_money}")
            # add to owned
            owned += 1
            # update cost
            cost *= 2
            # update labels
            labels[0].config(text=f"Cost: {cost}")
            labels[2].config(text=f"Owned: {owned}")

        self.store[item][0] = cost
        self.store[item][1] = cps
        self.store[item][2] = owned

    def update_cps(self):
        # add cps to total every second
        self.total_money += self.total_cps
        self.total.config(text=f"Total: {self.total_money}")
        self.window.after(1000, self.update_cps)

    def read_save(self, save):
        if save:
            self.total_money = save["total_money"]
            self.total_cps = save["total_cps"]
            self.click_value = save["click_value"]
            self.store = save["store"]
            return

        self.total_money = 0
        self.total_cps = 0
        self.click_value = 1
        self.store = {
            "Small clicker": [10, 1, 0],
            "Medium clicker": [1000, 100, 0],
            "Large clicker": [100000, 10000, 0],
        }

    def autosave(self):
        save = {
            "total_money": self.total_money,
            "total_cps": self.total_cps,
            "click_value": self.click_value,
            "store": self.store,
        }
        with open("save.json", "w") as f:
            json.dump(save, f)

        self.window.after(1000 * 10, self.autosave)


if __name__ == "__main__":
    try:
        with open("save.json", "r") as f:
            saved_game = f.read()
            Game(json.loads(saved_game))
    except FileNotFoundError:
        Game(None)
