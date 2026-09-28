// we gonna build a login board for our app 

export default function Home() {
  const backend_url = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3000';

return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <head>
        <title>Login Board</title>
        <link rel="icon" href="/favicon.ico" />
      </head>

      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-6xl font-bold">
          Welcome to the Login Board!
        </h1>

        <p className="mt-3 text-2xl">
          Get started by logging in below.
        </p>

        <div className="mt-6">
          <a
            href={`${backend_url}/auth/login`}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Login
          </a>
        </div>
      </main>
    </div>
  );
}
