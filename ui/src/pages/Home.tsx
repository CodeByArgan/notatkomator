import { useMutation, useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';

import { axiosGet, axiosPost } from '../utils';
import { BaseResponse, ListResponse } from '../api';
import { LoadingSpinner } from '../shared';

interface AuditLog {
  id: string;
  username: string;
  details: string;
  created_at: string;
}

export const HomePage = () => {
  const { data, isPending, refetch } = useQuery({
    queryKey: ['audit-logs'],
    queryFn: async () =>
      await axiosGet<ListResponse<AuditLog[]>>({ url: '/audit-log/list' }),
  });

  const createAuditLog = useMutation({
    mutationFn: async () =>
      await axiosPost<BaseResponse>({
        url: '/audit-log/test-create',
        data: {},
      }),
    onSuccess: () => {
      refetch();
    },
  });

  return (
    <>
      <h1 className="text-xl">Home page</h1>

      <h3>Audit logs list</h3>
      <div>
        <button
          className="cursor-pointer border-white border-1 p-2 rounded-sm hover:bg-white/10"
          onClick={() => createAuditLog.mutate()}
        >
          Add test audit log
        </button>
      </div>
      {isPending && <LoadingSpinner />}
      {!isPending &&
        data?.list.map((auditLog) => (
          <p key={auditLog.id}>
            {auditLog.username} [{format(auditLog.created_at, 'Pp')}]:{' '}
            {auditLog.details}{' '}
          </p>
        ))}
    </>
  );
};
