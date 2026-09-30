export const metadata = {
  title: 'Login Board'
};

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000';

export default function LoginPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <main className="flex flex-col items-center justify-center max-w-3xl mx-auto p-8 text-center">
        <h1 className="text-6xl font-bold">
          Welcome to the Login Board!
        </h1>

        <p className="mt-3 text-gray-600">
          Get started by logging in below.
        </p>

        <div className="mt-6">
          <a
            href={`${BACKEND_URL}/auth/google/login`}
            className="px-4 py-2 bg-black text-white rounded hover:bg-blue-600"
          >
            Login
          </a>
        </div>
      </main>
    </div>
  );
}