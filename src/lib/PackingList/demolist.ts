import type { ItemModel, PackingListModel } from "./models";

const item = (
  name: string,
  category: string,
  hasPacked: boolean = true,
  quantity: number = 1
): ItemModel => ({
  name: name,
  quantity: quantity,
  category: category,
  hasPacked: hasPacked,
});

export const demolist: PackingListModel = {
  title: "Laid-Back Camp",
  members: new Set([
    {
      name: "Nadeshiko Kagamihara",
      items: [
        item("Telt", "Søvn"),
        item("Sovepose", "Søvn"),
        item("Liggeunderlag", "Søvn"),
        item("Pute", "Søvn"),
        item("Pannekakemiks", "Mat"),
        item("Ketchup", "Mat"),
        item("Hot Pot", "Mat"),
        item("Seigmenn", "Snacks"),
        item("Kvikk Lunsj", "Snacks", true, 3),
        item("Melkesjokolade", "Snacks"),
        item("Chips", "Snacks"),
      ],
    },
    {
      name: "Rin Shima",
      items: [
        item("Telt", "Søvn"),
        item("Sovepose", "Søvn"),
        item("Liggeunderlag", "Søvn"),
        item("Pute", "Søvn"),
        item("Pølser", "Mat"),
        item("Pølsebrød", "Mat"),
      ],
    },
  ]),
};
