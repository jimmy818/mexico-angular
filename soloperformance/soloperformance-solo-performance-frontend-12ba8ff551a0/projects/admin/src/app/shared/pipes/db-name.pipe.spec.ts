import { DbNamePipe } from './db-name.pipe';

describe('DbNamePipe', () => {
  it('create an instance', () => {
    const pipe = new DbNamePipe();
    expect(pipe).toBeTruthy();
  });
});
