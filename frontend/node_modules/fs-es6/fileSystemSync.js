import window from '../global/window'
import FileReader from '../global/fileReader'
import FileWriterSync from './fileWriterSync'

export default class FileSystemSync {
  constructor(type = window.TEMPORARY, size = Math.pow(1024, 3)) {
    this.type = type
    this.size = size
  }

  get root() {
    if (this._root)
      return this._root

    const request = window.requestFileSystem ||
      window.webkitRequestFileSystem

    return new Promise((resolve, reject) =>
      request(this.type, this.size, fs =>
      resolve(this._root = Promise.resolve(fs.root)), reject))
  }

  async getFileEntry(path, config) {
    const root = await this.root
    return new Promise((resolve, reject) =>
      root.getFile(path, config, resolve, reject))
  }

  async getDirectoryEntry(path, {create, exclusive = true} = {}) {
    const root = await this.root
    return new Promise((resolve, reject) =>
      root.getDirectory(path, {create, exclusive}, resolve, reject))
  }

  async getFileReader(path) {
    const entry = await this.getFileEntry(path, {create: false})
    return new Promise((resolve, reject) => {
      entry.file(file => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader)
        reader.readAsText(file)
      }, reject)
    })
  }

  async getFileWriter(path, {create = true, exclusive = false} = {}) {
    const entry = await this.getFileEntry(path, {create, exclusive})
    return new Promise((resolve, reject) => entry.createWriter((writer) =>
      resolve(new FileWriterSync(writer, path)), reject))
  }
}
