/** Figure export helpers — serialise a rendered chart's <svg> for the thesis report. */

const serialize = (svg: SVGSVGElement): string => {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  return new XMLSerializer().serializeToString(clone);
};

const triggerDownload = (href: string, filename: string) => {
  const anchor = document.createElement("a");
  anchor.href = href;
  anchor.download = filename;
  anchor.click();
};

/** Downloads the chart inside `container` as a standalone vector SVG file. */
export const downloadSvg = (container: HTMLElement | null, filename: string) => {
  const svg = container?.querySelector("svg");
  if (!svg) {
    return;
  }
  const blob = new Blob([serialize(svg as SVGSVGElement)], { type: "image/svg+xml" });
  const url = URL.createObjectURL(blob);
  triggerDownload(url, filename);
  URL.revokeObjectURL(url);
};

/** Downloads the chart inside `container` as a white-background PNG (2x scale). */
export const downloadPng = (container: HTMLElement | null, filename: string) => {
  const svg = container?.querySelector("svg") as SVGSVGElement | null;
  if (!svg) {
    return;
  }
  const { width, height } = svg.getBoundingClientRect();
  const scale = 2;
  const data = serialize(svg);
  const image = new Image();
  image.onload = () => {
    const canvas = document.createElement("canvas");
    canvas.width = width * scale;
    canvas.height = height * scale;
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }
    ctx.scale(scale, scale);
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, width, height);
    ctx.drawImage(image, 0, 0);
    triggerDownload(canvas.toDataURL("image/png"), filename);
  };
  image.src = `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(data)))}`;
};
