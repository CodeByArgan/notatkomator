export interface ListResponse<T> {
  page: number;
  total: number;
  has_next: boolean;
  list: T;
}

export interface BaseResponse {
  message: 'ok' | 'error';
}
