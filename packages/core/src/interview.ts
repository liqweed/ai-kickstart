import { isSeparatorRow, tableCells } from "./text.ts";

export interface Round {
  n: number;
  name: string;
  goal: string;
  feeds: string;
}

/** Parse the rounds table of `vault/_system/kickstart/interview-protocol.md`. */
export function parseRounds(md: string): Round[] {
  const rounds: Round[] = [];
  for (const line of md.split(/\r?\n/)) {
    const cells = tableCells(line);
    if (!cells || cells.length !== 4 || isSeparatorRow(cells) || !/^\d+$/.test(cells[0])) continue;
    // [[round-1-landscape|Getting to know you]] -> Getting to know you
    const name = cells[1].replace(/\[\[[^|\]]*\|([^\]]+)\]\]/g, "$1").replace(/\[\[([^\]]+)\]\]/g, "$1");
    rounds.push({ n: Number(cells[0]), name, goal: cells[2], feeds: cells[3] });
  }
  return rounds;
}
