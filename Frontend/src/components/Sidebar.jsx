import { NavLink, useNavigate } from "react-router-dom";

export default function Sidebar({ onLogout }) {
    const navigate = useNavigate();

    const menuItems = [
        {
            name: "Dashboard",
            path: "/dashboard",
            icon: "📊"
        },
        {
            name: "Transactions",
            path: "/transactions",
            icon: "💳"
        },
        {
            name: "Budgets",
            path: "/budgets",
            icon: "💰"
        },
        {
            name: "Reports",
            path: "/reports",
            icon: "📈"
        }
    ];

    const handleLogout = () => {
        // Remove the login token and user ID from storage
        localStorage.removeItem("token");
        localStorage.removeItem("userId");

        // Call optional parent handler if provided
        if (onLogout) {
            onLogout();
        }

        // Navigate to login page
        navigate("/");
    };

    return (
        <div className="w-64 min-h-screen bg-gray-900 text-white p-5 flex flex-col justify-between shadow-lg">
          <div>
            {/* Application Logo */}
            <h1 className="text-2xl font-bold mb-10 flex items-center gap-2">
                <span>💰</span> Budget Tracker
            </h1>

            {/* Navigation Menu */}
            <nav className="space-y-3">
                {menuItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 p-3 rounded-lg transition-colors ${
                                isActive
                                    ? "bg-green-600 text-white font-medium"
                                    : "text-gray-300 hover:bg-gray-800 hover:text-white"
                            }`
                        }
                    >
                        <span className="text-xl">{item.icon}</span>
                        <span>{item.name}</span>
                    </NavLink>
                ))}
            </nav>
          </div>

          {/* Logout Button */}
          <button
              onClick={handleLogout}
              className="w-full p-3 bg-red-600 hover:bg-red-700 transition-colors rounded-lg flex items-center justify-center gap-2 font-medium"
          >
              <span>🚪</span> Logout
          </button>
        </div>
    );
}