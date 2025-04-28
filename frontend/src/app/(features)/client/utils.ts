import axiosInstance from "@/lib/axios-config";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const getProducts = async (token: string) => {
  console.log("Token:", token);
  const getProductsOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    url: `${BACKEND_URL}/api/v1/protected`,
  };

  try {
    const response = await axiosInstance.request(getProductsOptions);
    const {
      data: {
        payload: { items },
      },
    } = response;

    console.log("Products:", items);
    return items;
  } catch (error) {
    console.error("Error fetching products:", error);
    return null;
  }
};
