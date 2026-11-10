/**
 * Quiet data tables: sentence-case headers, hairline rows, room to read. The outer columns
 * carry no outside padding, so a table's text lines up with the heading above it.
 */
export const TABLE = "w-full border-collapse text-sm";
const CELL = "border-b border-(--line) px-3 first:pl-0 last:pr-0";
export const TH = `${CELL} py-2 text-left font-medium whitespace-nowrap text-(--muted)`;
export const TD = `${CELL} py-2.5 align-top`;
/** A row's leading cell, naming what the row is about. */
export const ROW_HEAD = `${TD} text-left font-medium text-(--ink)`;
export const LINK = "text-(--accent-deep) hover:underline";
