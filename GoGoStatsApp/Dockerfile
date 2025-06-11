FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 3040

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["GoGoStats.csproj", "."]
RUN dotnet restore "GoGoStats.csproj"
COPY . .
RUN dotnet build "GoGoStats.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "GoGoStats.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "GoGoStats.dll", "--urls=http://0.0.0.0:3040"]