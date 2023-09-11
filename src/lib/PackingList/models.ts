export type PackingListModel = {
  title: string;
  members: Set<MemberModel>;
  categories?: Set<string>;
};

export type MemberModel = {
  name: string;
  items: ItemModel[];
};

export type ItemModel = {
  name: string;
  category: string;
  quantity: number;
  hasPacked: boolean;
};
