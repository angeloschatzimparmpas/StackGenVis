export * from "./gl3";
export * from "./graphics";

export let kInfo: number;
export let kWarning: number;
export let kError: number;
export let kFatal: number;
export function log(level: number, text: string): void;

export class OpenGLWindow {
    constructor(info: {
        config?: string;
        title?: string;
        width?: number;
        height?: number;
        active_stereo?: boolean;
        hide_cursor?: boolean;
        fullscreen?: boolean;
    });
    public onResize(callback: (width: number, height: number) => void): void;
    public onClose(callback: () => void): void;
    public onRefresh(callback: () => void): void;
    public onFocus(callback: (isFocused: boolean) => void): void;
    public onIconify(callback: (isIconified: boolean) => void): void;
    public onFramebufferSize(callback: (width: number, height: number) => void): void;
    public onMove(callback: (x: number, y: number) => void): void;
    public onKeyboard(callback: (key: string, action: string, modifiers: string, scancode: number) => void): void;
    public makeContextCurrent(): void;
    public swapBuffers(): void;
    public setSwapInterval(interval: number): void;
    public pollEvents(): void;
    public waitEvents(): void;
    public getFramebufferSize(): [ number, number ];
    public shouldClose(): boolean;
    public close(): void;
}

export interface ICompositeInfo {
    panorama?: [ number, number, "cubemap" | "cubemap-yuv420p" | "equirectangular" ];
}

export interface IOmniStereo {
    setPose: (x: number, y: number, z: number, qx: number, qy: number, qz: number, qw: number) => void;
    setLens: (eyeSeparation: number, sphereRadius: number) => void;
    setClipRange: (near: number, far: number) => void;
    getCubemapTexture: () => [ number, number ];
    getDepthCubemapTexture: () => [ number, number ];
    capture: () => void;
    composite: (viewportX: number, viewportY: number, viewportWidth: number, viewportHeight: number, compositeInfo: ICompositeInfo) => void;
    setUniforms: (shaderID: number) => void;
    getShaderCode: () => string;
    compositeCustomizeShader: (code: string) => void;
    compositeRestoreShader: () => void;
    onCaptureViewport: (callback: () => void) => void;
    getHeadPose?: () => number[];
}

export class OmniStereo {
    constructor(config?: string);
    public setPose(x: number, y: number, z: number, qx: number, qy: number, qz: number, qw: number): void;
    public setLens(eyeSeparation: number, sphereRadius: number): void;
    public setClipRange(near: number, far: number): void;
    public getCubemapTexture(): [ number, number ];
    public getDepthCubemapTexture(): [ number, number ];
    public capture(): void;
    public composite(viewportX: number, viewportY: number, viewportWidth: number, viewportHeight: number, compositeInfo: ICompositeInfo): void;
    public setUniforms(shaderID: number): void;
    public getShaderCode(): string;
    public compositeCustomizeShader(code: string): void;
    public compositeRestoreShader(): void;
    public onCaptureViewport(callback: () => void): void;
}

export module OpenVR {
    export class OmniStereo {
        constructor();
        public setPose(x: number, y: number, z: number, qx: number, qy: number, qz: number, qw: number): void;
        public setLens(eyeSeparation: number, sphereRadius: number): void;
        public setClipRange(near: number, far: number): void;
        public getCubemapTexture(): [ number, number ];
        public getDepthCubemapTexture(): [ number, number ];
        public capture(): void;
        public composite(viewportX: number, viewportY: number, viewportWidth: number, viewportHeight: number, compositeInfo: ICompositeInfo): void;
        public setUniforms(shaderID: number): void;
        public getShaderCode(): string;
        public compositeCustomizeShader(code: string): void;
        public compositeRestoreShader(): void;
        public onCaptureViewport(callback: () => void): void;
        public getHeadPose(): number[];
    }
}