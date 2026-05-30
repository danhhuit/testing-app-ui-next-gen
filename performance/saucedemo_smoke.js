import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '20s', target: 5 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate>0.95'],
  },
};

export default function () {
  const res = http.get('https://www.saucedemo.com/');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'page contains Swag Labs': (r) => r.body.includes('Swag Labs'),
  });

  sleep(1);
}