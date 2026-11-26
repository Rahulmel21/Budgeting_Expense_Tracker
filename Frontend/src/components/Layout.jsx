
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout({ children }) {

    return (

        <div className="flex min-h-screen bg-gray-100">

            {/* Sidebar */}
            <Sidebar />

            {/* Main Content */}
            <div className="flex-1">

                {/* Navbar */}
                <Navbar />

                {/* Page Content */}
                <main className="p-6">

                    {children}

                </main>

            </div>

        </div>
    );
}

export default Layout;
