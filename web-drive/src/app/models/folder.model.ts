export interface Folder {
    type: string,
    name: string,
    directories: (File|Folder)[]
}
