function Navbar() {
  return (
    <div className="w-full bg-white shadow-sm p-5 flex justify-between items-center">
      {/* Page Heading */}
      <div>
        <h2 className="text-xl font-bold text-gray-800">
          Personal Finance Management
        </h2>
        <p className="text-sm text-gray-500">
          Manage your income and expenses
        </p>
      </div>

      {/* User Information */}
      <div className="flex items-center gap-3">
        <div className="text-right">
          <p className="font-semibold text-gray-800">
            My Account
          </p>
          <p className="text-sm text-gray-500">
            User
          </p>
        </div>

        <div className="w-10 h-10 bg-green-600 text-white rounded-full flex items-center justify-center font-bold">
          U
        </div>
      </div>
    </div>
  );
}

export default Navbar;