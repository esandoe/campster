<script lang="ts">
  import Heading from "../ui/Heading.svelte";
  import Section from "../ui/Section.svelte";
  import type { ItemModel, MemberModel, PackingListModel } from "./models";
  import { Avatar, Checkbox } from "flowbite-svelte";

  export let packingList: PackingListModel;

  function merge(
    list: PackingListModel
  ): Map<string, Map<string, [MemberModel, ItemModel][]>> {
    if (!list) return new Map();

    const categoryItems = new Map();

    for (const member of list.members) {
      for (const item of member.items) {
        if (!categoryItems.has(item.category))
          categoryItems.set(item.category, new Map());

        let items = categoryItems.get(item.category);

        if (!items.has(item.name)) items.set(item.name, []);
        items.get(item.name).push([member, item]);
      }
    }

    return categoryItems;
  }

  function getInitials(name: string): string {
    const parts = name.toUpperCase().split(" ");
    if (parts.length > 1) return parts[0][0] + parts[parts.length - 1][0];
    return parts[0][0] + parts[0][1];
  }

  const colors = [
    "#DAAAC6",
    "#896CC1",
    "#2B88AB",
    "#C58BCD",
    "#4C60B6",
    "#E7C9CB",
  ];

  $: categoryMap = merge(packingList);
  $: members = [...packingList.members].map((member) => member.name);
  $: avatarColor = new Map(
    [...packingList.members].map((m, i) => [m.name, colors[i]])
  );
</script>

<Section>
  <Heading size="lg">Pakkeliste</Heading>

  Deltakere i listen:
  <div>
    {#each members as member}
      <div style:display="flex" style:align-items="center">
        <div
          class="avatar dot"
          style:background-color={avatarColor.get(member)}
        >
          {getInitials(member)}
        </div>
        {member}
      </div>
    {/each}
  </div>

  <div style="display: flex; flex-direction: column; gap: 1em;">
    {#each [...categoryMap] as [category, itemMap]}
      <Heading size="sm">{category}</Heading>
      {#each [...itemMap] as [itemName, memberList], index}
        <div class="item" class:first={index === 0}>
          <Checkbox>
            {itemName}
          </Checkbox>
          <span style:flex="1" />

          {#each memberList as [member, item]}
            <Avatar class="bg-red">{getInitials(member.name)}</Avatar>
            <!-- <div
              class="avatar"
              style:background-color={avatarColor.get(member.name)}
            >
              {getInitials(member.name)}
            </div> -->
          {/each}
        </div>
      {/each}
    {/each}
  </div>
</Section>

<style>
  .item {
    display: flex;
    width: 100%;
    align-items: center;
    border-bottom: 1px solid var(--dark-accent);
    padding-block: 0.5em;
    margin-block: 0;
  }

  .item.first {
    border-top: 1px solid var(--dark-accent);
  }
  /* 
  .avatar {
    display: inline-block;

    --size: 30px;
    height: var(--size);
    width: var(--size);
    border-radius: calc(var(--size) / 2);
    line-height: var(--size);
    text-align: center;
    color: var(--light);
    border: none;
    font-size: calc(var(--size) / 2.5);
    margin-inline: 4px;

    transition: width linear 0.05s;
  }

  .avatar.dot {
    --size: 7px;
    content-visibility: hidden;
  } */
</style>
