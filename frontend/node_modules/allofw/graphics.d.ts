export module graphics {

    export let SURFACETYPE_PDF: number;
    export let SURFACETYPE_RASTER: number;
    export let LINECAP_BUTT: number;
    export let LINECAP_ROUND: number;
    export let LINECAP_SQUARE: number;
    export let LINEJOIN_BEVEL: number;
    export let LINEJOIN_MITER: number;
    export let LINEJOIN_ROUND: number;
    export let FONTSTYLE_NORMAL: number;
    export let FONTSTYLE_BOLD: number;
    export let FONTSTYLE_ITALIC: number;
    export let FONTSTYLE_BOLDITALIC: number;
    export let TEXTALIGN_LEFT: number;
    export let TEXTALIGN_CENTER: number;
    export let TEXTALIGN_RIGHT: number;
    export let PAINTMODE_STROKE: number;
    export let PAINTMODE_FILL: number;
    export let PAINTMODE_STROKEFILL: number;
    export let TRANSFERMODE_SRC_OVER: number;

    export class Surface2D {
        constructor(data: ArrayBufferView);
        constructor(width: number, height: number, data: ArrayBufferView);
        constructor(width: number, height: number, type: number);

        public width(): number;
        public height(): number;
        public pixels(): ArrayBufferView;
        public bindTexture(textureUnit: number): void;
        public uploadTexture(): void;
        public unbindTexture(textureUnit: number): void;
        public save(filename: string): void;
    }

    export class VideoSurface2D {
        constructor(filename: string);

        public width(): number;
        public height(): number;
        public fps(): number;
        public duration(): number;
        public nextFrame(): void;
        public seek(timestamp: number): void;
        public pixels(): ArrayBufferView;
        public setPixelBuffer(buffer: ArrayBufferView): void;
    }

    export class Path2D {
        public moveTo(x: number, y: number): Path2D;
        public lineTo(x: number, y: number): Path2D;
        public bezierCurveTo(c1x: number, c1y: number, c2x: number, c2y: number, x: number, y: number): Path2D;
        public circle(cx: number, cy: number, radius: number): Path2D;
        public arc(cx: number, cy: number, radius: number, angle1: number, angle2: number): Path2D;
        public close(): Path2D;
    }

    export class Paint2D {
        public setMode(mode: number): Paint2D;
        public setColor(r: number, g: number, b: number, a?: number): Paint2D;
        public setStrokeWidth(width: number): Paint2D;
        public setLineCap(lineCap: number): Paint2D;
        public setLineJoin(lineJoin: number): Paint2D;

        public setTextSize(textSize: number): Paint2D;
        public setTextAlign(textAlign: number): Paint2D;
        public setTypeface(fontFamily: string, fontStyle?: number): Paint2D;

        public measureText(text: string): number;

        public setColorMatrix(...args: number[]): Paint2D;
        public setColorMatrixScale(r: number, g: number, b: number, a: number): Paint2D;
        public setColorMatrixScaleAlpha(alpha: number): Paint2D;
        public setTransferMode(mode: number): Paint2D;

        public clone(): Paint2D;
    }

    export class GraphicalContext2D {
        constructor(surface: Surface2D);

        public path(): Path2D;
        public paint(): Paint2D;
        public drawPath(path: Path2D, paint: Paint2D): void;
        public drawText(text: string, x: number, y: number, paint: Paint2D): void;
        public drawLine(x1: number, y1: number, x2: number, y2: number, paint: Paint2D): void;
        public drawCircle(cx: number, cy: number, radius: number, paint: Paint2D): void;
        public drawRectangle(x: number, y: number, width: number, height: number, paint: Paint2D): void;
        public drawSurface(surface: Surface2D | VideoSurface2D, x: number, y: number, paint: Paint2D): void;
        public drawSurface(surface: Surface2D | VideoSurface2D, sx: number, sy: number, sw: number, sh: number, dx: number, dy: number, dw: number, dh: number, paint: Paint2D): void;
        public rotate(angle: number): void;
        public translate(tx: number, ty: number): void;
        public scale(sx: number, sy: number): void;
        public concatTransform(a: number, b: number, c: number, d: number, e: number, f: number): void;
        public setTransform(a: number, b: number, c: number, d: number, e: number, f: number): void;
        public getTransform(): [ number, number, number, number, number, number ];

        public clear(r: number, g: number, b: number, a?: number): void;
        public reset(): void;

        public save(): void;
        public restore(): void;

        public flush(): void;
    }

    export function loadImageData(data: ArrayBufferView): Surface2D;
}