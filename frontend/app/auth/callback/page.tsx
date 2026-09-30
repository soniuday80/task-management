'use client'; // forgot this one too lol
export const dynamic = 'force-dynamic'; // rendering it live 
import { useEffect , Suspense } from 'react';
import { useRouter , useSearchParams } from 'next/navigation';
import { getUserIdFromToken } from '@/lib/jwt';


function CallbackHandler() {

// we need an acces token to access the backend api, so we will get it from the url query params and store it in local storage
    const router = useRouter();
    const  searchParams  = useSearchParams();



    useEffect(() => {
        if (searchParams) {
            const accessToken = searchParams.get('acces_token');
            if (accessToken) {
                localStorage.setItem('access_token', accessToken);
                const user_id = getUserIdFromToken(accessToken);
                if (user_id) localStorage.setItem('user_id', user_id);
                 router.push('/dashboard');
            }
        }
    }, [searchParams, router]); // we need to add searchParams and router as dependencies to the useEffect hook, so that it runs again when they change

    
return (
        <div className="flex h-screen items-center justify-center">
            <p>Processing your login...</p>
        </div>
    );

}




export default function AuthCallback() {
    return (
        <Suspense fallback={
            <div className="flex h-screen items-center justify-center">
                <p>Loading authentication...</p>
            </div>
        }>
            <CallbackHandler />
        </Suspense>
    );
}