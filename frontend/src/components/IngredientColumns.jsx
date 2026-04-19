function IngredientColumns({ generally_recognised = [], worth_knowing = [], commonly_questioned = [] }) {
  const Column = ({ title, subtitle, description, bgColor, borderColor, icon, ingredients }) => (
    <div className="flex flex-col">
      <div className={`${bgColor} rounded-t-xl p-4 flex items-center gap-3`}>
        {icon}
        <div>
          <h3 className="font-poppins font-semibold text-lg">{title}</h3>
          <p className="text-xs text-gray-600">{subtitle}</p>
        </div>
      </div>
      <div className={`border-l-4 ${borderColor} bg-gray-50 px-4 py-3`}>
        <p className="text-xs text-gray-500 leading-relaxed">{description}</p>
      </div>
      <div className="bg-white rounded-b-xl border border-t-0 border-gray-200 p-4 space-y-2 min-h-[200px]">
        {ingredients.length === 0 ? (
          <p className="text-sm text-gray-400 italic">None found</p>
        ) : (
          ingredients.map((ing, idx) => (
            <div 
              key={idx} 
              className="p-3 bg-gray-50 rounded-lg hover:shadow-sm transition-shadow cursor-pointer"
            >
              <p className="font-medium text-sm">{ing.name}</p>
              {ing.one_line_note && (
                <p className="text-xs text-gray-500 mt-1">{ing.one_line_note}</p>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Column
        title="Generally Recognised"
        subtitle="Ingredients with no notable regulatory flags"
        description="Safe ingredients with no known adverse effects at normal consumption levels. Approved by major regulatory bodies worldwide without restrictions."
        bgColor="bg-green-50"
        borderColor="border-green-400"
        icon={
          <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        }
        ingredients={generally_recognised}
      />
      <Column
        title="Worth Knowing"
        subtitle="Permitted but discussed in research"
        description="Ingredients with some concerns or restrictions. May cause issues in sensitive individuals or at high doses. Mixed scientific findings — fine for most people in small amounts."
        bgColor="bg-amber-50"
        borderColor="border-amber-400"
        icon={
          <svg className="w-6 h-6 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        }
        ingredients={worth_knowing}
      />
      <Column
        title="Commonly Questioned"
        subtitle="Flagged or restricted in some countries"
        description="Ingredients flagged, restricted, or banned in one or more countries. Associated with potential health concerns — worth avoiding or limiting where possible."
        bgColor="bg-red-50"
        borderColor="border-red-400"
        icon={
          <svg className="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a1 1 0 11-2 0V6z" clipRule="evenodd" />
          </svg>
        }
        ingredients={commonly_questioned}
      />
    </div>
  )
}

export default IngredientColumns
