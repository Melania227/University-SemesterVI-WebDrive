import { Folder } from "./folder.model";

export interface User {
    user: string,
    maxBytes: number,
    currentBytes: number,
    root: Folder,
    shared: Folder
}
